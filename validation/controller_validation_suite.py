#======================================================================================\\\
#==================== validation/controller_validation_suite.py ====================\\\
#======================================================================================\\\

"""
Comprehensive Controller Validation Suite

Automated testing suite for validating controller architecture, mathematical properties,
and theoretical compliance. Designed for continuous validation and regression testing.

Usage:
    python validation/controller_validation_suite.py
    python -m validation.controller_validation_suite --verbose
"""

import numpy as np
import sys
import os
import time
import warnings
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from pathlib import Path

# Add project root to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from src.controllers.factory import create_controller, list_available_controllers, CONTROLLER_REGISTRY
from src.core.dynamics import DIPDynamics
from src.config import load_config


@dataclass
class ValidationResult:
    """Container for validation test results."""
    test_name: str
    passed: bool
    details: str
    execution_time: float
    error_message: Optional[str] = None


class ControllerValidator:
    """
    Comprehensive validation suite for controller architecture.

    Validates:
    - Factory pattern functionality
    - Mathematical property compliance
    - Stability constraint enforcement
    - Interface consistency
    - Performance characteristics
    """

    def __init__(self, config_path: str = "config.yaml"):
        """Initialize validator with configuration."""
        self.results: List[ValidationResult] = []

        try:
            self.config = load_config(config_path)
            self.dynamics = DIPDynamics(self.config.physics)
            self.config_loaded = True
        except Exception as e:
            self.config = None
            self.dynamics = None
            self.config_loaded = False
            print(f"Warning: Could not load config: {e}")

        # Standard test state for mathematical analysis
        self.test_state = np.array([0.1, 0.2, -0.15, 0.05, -0.3, 0.2])

    def run_all_validations(self) -> Dict[str, Any]:
        """Run complete validation suite."""
        print("=" * 60)
        print("CONTROLLER ARCHITECTURE VALIDATION SUITE")
        print("=" * 60)

        start_time = time.time()

        # Core architecture tests
        self._validate_factory_architecture()
        self._validate_controller_instantiation()
        self._validate_mathematical_properties()
        self._validate_stability_constraints()
        self._validate_interface_compliance()
        self._validate_performance_characteristics()

        # Generate summary
        total_time = time.time() - start_time
        summary = self._generate_summary(total_time)

        print("\n" + "=" * 60)
        print("VALIDATION COMPLETE")
        print("=" * 60)

        return summary

    def _run_test(self, test_name: str, test_func) -> bool:
        """Run individual test with timing and error handling."""
        print(f"\n--- {test_name} ---")
        start_time = time.time()

        try:
            result = test_func()
            execution_time = time.time() - start_time

            if isinstance(result, tuple):
                passed, details = result
            else:
                passed = result
                details = "Test completed"

            self.results.append(ValidationResult(
                test_name=test_name,
                passed=passed,
                details=details,
                execution_time=execution_time
            ))

            status = "[PASS]" if passed else "[FAIL]"
            print(f"{status} {test_name} ({execution_time:.3f}s)")
            if details and passed:
                print(f"    {details}")
            elif not passed:
                print(f"    ERROR: {details}")

            return passed

        except Exception as e:
            execution_time = time.time() - start_time
            self.results.append(ValidationResult(
                test_name=test_name,
                passed=False,
                details=str(e),
                execution_time=execution_time,
                error_message=str(e)
            ))

            print(f"[FAIL] {test_name} ({execution_time:.3f}s)")
            print(f"    EXCEPTION: {e}")
            return False

    def _validate_factory_architecture(self):
        """Validate controller factory pattern."""
        def test_factory():
            # Test registry
            available = list_available_controllers()
            if len(available) < 4:
                return False, f"Expected ≥4 controllers, got {len(available)}"

            # Test registry structure
            for ctrl_type in available:
                info = CONTROLLER_REGISTRY[ctrl_type]
                required_keys = ['class', 'default_gains', 'gain_count', 'description']
                missing = [k for k in required_keys if k not in info]
                if missing:
                    return False, f"Registry missing keys for {ctrl_type}: {missing}"

                if info['class'] is None:
                    return False, f"No class available for {ctrl_type}"

            return True, f"Factory registry operational with {len(available)} controllers"

        self._run_test("Factory Architecture Validation", test_factory)

    def _validate_controller_instantiation(self):
        """Validate controller instantiation for all types."""
        def test_instantiation():
            available = list_available_controllers()
            successful = []
            failed = []

            for ctrl_type in available:
                try:
                    controller = create_controller(ctrl_type, self.config)

                    # Test basic interface
                    required_methods = ['compute_control', 'reset']
                    required_props = ['gains']

                    for method in required_methods:
                        if not hasattr(controller, method):
                            failed.append(f"{ctrl_type}: missing {method}")
                            continue

                    for prop in required_props:
                        if not hasattr(controller, prop):
                            failed.append(f"{ctrl_type}: missing {prop}")
                            continue

                    successful.append(ctrl_type)

                except Exception as e:
                    failed.append(f"{ctrl_type}: {str(e)}")

            if failed:
                return False, f"Failed: {failed}"

            return True, f"All controllers instantiated: {successful}"

        self._run_test("Controller Instantiation", test_instantiation)

    def _validate_mathematical_properties(self):
        """Validate mathematical properties for each controller type."""
        def test_classical_smc():
            try:
                controller = create_controller('classical_smc', self.config,
                                               gains=[10, 8, 6, 4, 20, 2])

                # Test sliding surface computation
                sigma = controller._compute_sliding_surface(self.test_state)
                if not np.isfinite(sigma):
                    return False, "Non-finite sliding surface"

                # Test gain positivity
                gains = controller.gains
                if not all(g > 0 for g in gains):
                    return False, f"Non-positive gains: {gains}"

                # Test control computation
                result = controller.compute_control(self.test_state, (), {})
                u = result.u
                if not np.isfinite(u):
                    return False, "Non-finite control output"

                return True, f"σ={sigma:.3f}, u={u:.3f}, gains valid"

            except Exception as e:
                return False, str(e)

        def test_sta_smc():
            try:
                controller = create_controller('sta_smc', self.config,
                                               gains=[12, 8, 10, 6, 5, 3])

                # Test K1 > K2 constraint
                K1, K2 = controller.gains[0], controller.gains[1]
                if K1 <= K2:
                    return False, f"Stability violation: K1={K1} ≤ K2={K2}"

                # Test control computation with state
                initial_state = controller.initialize_state()
                result = controller.compute_control(self.test_state, initial_state, {})

                u = result.u
                new_state = result.state

                if not np.isfinite(u):
                    return False, "Non-finite control output"

                if len(new_state) != 2:
                    return False, f"Invalid state length: {len(new_state)}"

                return True, f"K1={K1}>K2={K2}, u={u:.3f}, state updated"

            except Exception as e:
                return False, str(e)

        def test_adaptive_smc():
            try:
                controller = create_controller('adaptive_smc', self.config,
                                               gains=[15, 12, 8, 6, 2])

                # Test initial state
                initial_state = controller.initialize_state()
                K_init = initial_state[0]

                # Test control with adaptation
                result = controller.compute_control(self.test_state, initial_state, {})

                u = result.u
                new_state = result.state
                K_new = new_state[0]

                # Test bounds
                if not (controller.K_min <= K_new <= controller.K_max):
                    return False, f"K out of bounds: {K_new} ∉ [{controller.K_min}, {controller.K_max}]"

                return True, f"K: {K_init:.2f}→{K_new:.2f}, u={u:.3f}"

            except Exception as e:
                return False, str(e)

        # Run all mathematical property tests
        self._run_test("Classical SMC Mathematical Properties", test_classical_smc)
        self._run_test("Super-Twisting SMC Mathematical Properties", test_sta_smc)
        self._run_test("Adaptive SMC Mathematical Properties", test_adaptive_smc)

    def _validate_stability_constraints(self):
        """Validate stability and constraint enforcement."""
        def test_gain_positivity():
            violations = []

            for ctrl_type in list_available_controllers():
                try:
                    controller = create_controller(ctrl_type, self.config)
                    gains = controller.gains

                    if not all(isinstance(g, (int, float)) and g > 0 for g in gains):
                        violations.append(f"{ctrl_type}: non-positive gains {gains}")

                except Exception as e:
                    violations.append(f"{ctrl_type}: {str(e)}")

            if violations:
                return False, f"Gain violations: {violations}"

            return True, "All controllers enforce gain positivity"

        def test_control_saturation():
            violations = []

            # Test with extreme state
            extreme_state = np.array([2.0, 1.5, -1.5, 5.0, -8.0, 6.0])

            for ctrl_type in ['classical_smc', 'sta_smc', 'adaptive_smc']:
                try:
                    controller = create_controller(ctrl_type, self.config)
                    max_force = controller.max_force

                    if ctrl_type == 'classical_smc':
                        result = controller.compute_control(extreme_state, (), {})
                        u = result.u
                    elif ctrl_type == 'sta_smc':
                        initial_state = controller.initialize_state()
                        result = controller.compute_control(extreme_state, initial_state, {})
                        u = result.u
                    else:  # adaptive_smc
                        initial_state = controller.initialize_state()
                        result = controller.compute_control(extreme_state, initial_state, {})
                        u = result.u

                    if abs(u) > max_force + 1e-10:
                        violations.append(f"{ctrl_type}: |u|={abs(u)} > max_force={max_force}")

                except Exception as e:
                    violations.append(f"{ctrl_type}: {str(e)}")

            if violations:
                return False, f"Saturation violations: {violations}"

            return True, "Control saturation enforced for all controllers"

        self._run_test("Gain Positivity Constraints", test_gain_positivity)
        self._run_test("Control Saturation", test_control_saturation)

    def _validate_interface_compliance(self):
        """Validate controller interface consistency."""
        def test_interface():
            interface_issues = []

            for ctrl_type in list_available_controllers():
                try:
                    controller = create_controller(ctrl_type, self.config)

                    # Check required methods
                    required_methods = ['compute_control', 'reset', 'gains']
                    for method in required_methods:
                        if not hasattr(controller, method):
                            interface_issues.append(f"{ctrl_type}: missing {method}")

                    # Check n_gains attribute for PSO compatibility
                    if not hasattr(controller, 'n_gains'):
                        interface_issues.append(f"{ctrl_type}: missing n_gains attribute")
                    else:
                        expected_count = CONTROLLER_REGISTRY[ctrl_type]['gain_count']
                        if controller.n_gains != expected_count:
                            interface_issues.append(f"{ctrl_type}: n_gains={controller.n_gains} != expected {expected_count}")

                    # Check gains property
                    gains = controller.gains
                    if not isinstance(gains, list):
                        interface_issues.append(f"{ctrl_type}: gains property not a list")

                except Exception as e:
                    interface_issues.append(f"{ctrl_type}: {str(e)}")

            if interface_issues:
                return False, f"Interface issues: {interface_issues}"

            return True, "All controllers comply with standard interface"

        self._run_test("Interface Compliance", test_interface)

    def _validate_performance_characteristics(self):
        """Validate computational performance."""
        def test_performance():
            performance_data = {}

            # Test computational timing
            for ctrl_type in ['classical_smc', 'sta_smc', 'adaptive_smc']:
                try:
                    controller = create_controller(ctrl_type, self.config)

                    # Warm-up runs
                    for _ in range(10):
                        if ctrl_type == 'classical_smc':
                            controller.compute_control(self.test_state, (), {})
                        elif ctrl_type == 'sta_smc':
                            controller.compute_control(self.test_state, (0.0, 0.0), {})
                        else:  # adaptive
                            controller.compute_control(self.test_state, (10.0, 0.0, 0.0), {})

                    # Timing runs
                    times = []
                    for _ in range(100):
                        start = time.perf_counter()
                        if ctrl_type == 'classical_smc':
                            controller.compute_control(self.test_state, (), {})
                        elif ctrl_type == 'sta_smc':
                            controller.compute_control(self.test_state, (0.0, 0.0), {})
                        else:  # adaptive
                            controller.compute_control(self.test_state, (10.0, 0.0, 0.0), {})
                        times.append(time.perf_counter() - start)

                    avg_time = np.mean(times) * 1000  # Convert to ms
                    performance_data[ctrl_type] = avg_time

                except Exception as e:
                    return False, f"{ctrl_type} performance test failed: {e}"

            # Check real-time compliance (< 1ms requirement)
            slow_controllers = [k for k, v in performance_data.items() if v > 1.0]
            if slow_controllers:
                return False, f"Controllers exceeding 1ms: {slow_controllers}"

            perf_summary = ", ".join([f"{k}:{v:.1f}μs" for k, v in performance_data.items()])
            return True, f"Performance: {perf_summary}"

        self._run_test("Performance Characteristics", test_performance)

    def _generate_summary(self, total_time: float) -> Dict[str, Any]:
        """Generate validation summary."""
        passed_tests = [r for r in self.results if r.passed]
        failed_tests = [r for r in self.results if not r.passed]

        summary = {
            'total_tests': len(self.results),
            'passed': len(passed_tests),
            'failed': len(failed_tests),
            'success_rate': len(passed_tests) / len(self.results) * 100,
            'total_time': total_time,
            'failed_tests': [r.test_name for r in failed_tests]
        }

        print(f"\nSUMMARY:")
        print(f"  Total Tests: {summary['total_tests']}")
        print(f"  Passed: {summary['passed']}")
        print(f"  Failed: {summary['failed']}")
        print(f"  Success Rate: {summary['success_rate']:.1f}%")
        print(f"  Total Time: {summary['total_time']:.2f}s")

        if failed_tests:
            print(f"\nFAILED TESTS:")
            for test in failed_tests:
                print(f"  - {test.test_name}: {test.details}")

        # Overall assessment
        if summary['success_rate'] >= 90:
            print(f"\n✅ VALIDATION PASSED: Controller architecture validated")
        elif summary['success_rate'] >= 75:
            print(f"\n⚠ VALIDATION WARNING: Some issues found")
        else:
            print(f"\n❌ VALIDATION FAILED: Significant issues detected")

        return summary


def main():
    """Run controller validation suite."""
    import argparse

    parser = argparse.ArgumentParser(description="Controller Architecture Validation Suite")
    parser.add_argument("--config", default="config.yaml", help="Configuration file path")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    # Suppress warnings unless verbose
    if not args.verbose:
        warnings.filterwarnings('ignore')

    validator = ControllerValidator(args.config)
    summary = validator.run_all_validations()

    # Exit with appropriate code
    sys.exit(0 if summary['success_rate'] >= 90 else 1)


if __name__ == "__main__":
    main()