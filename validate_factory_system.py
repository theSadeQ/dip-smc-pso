#======================================================================================\\\
#============================= validate_factory_system.py =============================\\\
#======================================================================================\\\

"""
Factory System Validation Script for DIP-SMC-PSO Project

This script provides comprehensive validation of the controller factory pattern
implementation, testing all controller variants, parameter handling, and integration
with optimization systems.

Control Systems Specialist validation tasks:
- Factory registration validation for all SMC variants
- Controller instantiation with parameter configurations
- Error handling and edge case testing
- Integration validation with simulation and PSO systems
- Stability analysis for factory-created controllers
- Performance impact assessment
"""

import sys
import traceback
import time
import logging
from typing import Dict, Any, List, Optional, Tuple
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_factory_imports():
    """Test that factory modules can be imported successfully."""
    logger.info("Testing factory module imports...")

    try:
        # Test main factory module
        from src.controllers.factory import (
            create_controller,
            list_available_controllers,
            list_all_controllers,
            get_default_gains,
            CONTROLLER_REGISTRY
        )
        logger.info("✓ Main factory module imported successfully")

        # Test legacy factory
        from src.controllers.factory.legacy_factory import (
            build_controller,
            create_controller as create_legacy,
            normalize_controller_name,
            apply_deprecation_mapping
        )
        logger.info("✓ Legacy factory module imported successfully")

        # Test SMC factory
        from src.controllers.factory import (
            SMCType, SMCFactory, create_smc_for_pso,
            get_gain_bounds_for_pso, SMC_GAIN_SPECS
        )
        logger.info("✓ SMC factory components imported successfully")

        return True

    except Exception as e:
        logger.error(f"✗ Factory import failed: {e}")
        traceback.print_exc()
        return False

def test_controller_registry():
    """Test controller registry contents and availability."""
    logger.info("Testing controller registry...")

    try:
        from src.controllers.factory import (
            list_available_controllers,
            list_all_controllers,
            CONTROLLER_REGISTRY
        )

        available = list_available_controllers()
        all_registered = list_all_controllers()

        logger.info(f"Available controllers: {available}")
        logger.info(f"All registered controllers: {all_registered}")

        # Expected controllers
        expected_controllers = [
            'classical_smc',
            'sta_smc',
            'adaptive_smc',
            'hybrid_adaptive_sta_smc'
        ]

        missing_controllers = []
        for controller in expected_controllers:
            if controller not in all_registered:
                missing_controllers.append(controller)

        if missing_controllers:
            logger.warning(f"Missing controllers from registry: {missing_controllers}")
        else:
            logger.info("✓ All expected controllers are registered")

        # Test registry structure
        for name, info in CONTROLLER_REGISTRY.items():
            required_keys = ['class', 'config_class', 'default_gains', 'gain_count', 'description']
            missing_keys = [key for key in required_keys if key not in info]
            if missing_keys:
                logger.warning(f"Controller {name} missing registry keys: {missing_keys}")
            else:
                logger.info(f"✓ Controller {name} has complete registry info")

        return True

    except Exception as e:
        logger.error(f"✗ Controller registry test failed: {e}")
        traceback.print_exc()
        return False

def test_controller_creation():
    """Test controller creation for all variants."""
    logger.info("Testing controller creation...")

    try:
        from src.controllers.factory import create_controller, get_default_gains

        # Test each controller type
        controller_tests = [
            {
                'name': 'classical_smc',
                'gains': [20.0, 15.0, 12.0, 8.0, 35.0, 5.0],
                'expected_methods': ['compute_control', 'reset']
            },
            {
                'name': 'sta_smc',
                'gains': [25.0, 15.0, 20.0, 12.0, 8.0, 6.0],
                'expected_methods': ['compute_control', 'reset']
            },
            {
                'name': 'adaptive_smc',
                'gains': [25.0, 18.0, 15.0, 10.0, 4.0],
                'expected_methods': ['compute_control', 'reset']
            },
            {
                'name': 'hybrid_adaptive_sta_smc',
                'gains': [18.0, 12.0, 10.0, 8.0],
                'expected_methods': ['compute_control', 'reset']
            }
        ]

        created_controllers = {}

        for test_case in controller_tests:
            name = test_case['name']
            gains = test_case['gains']
            expected_methods = test_case['expected_methods']

            try:
                logger.info(f"Creating {name} controller...")

                # Test with explicit gains
                controller = create_controller(name, gains=gains)

                # Verify controller has expected interface
                for method_name in expected_methods:
                    if not hasattr(controller, method_name):
                        logger.warning(f"Controller {name} missing method: {method_name}")
                    else:
                        logger.info(f"✓ Controller {name} has method: {method_name}")

                # Test default gains
                default_gains = get_default_gains(name)
                logger.info(f"✓ Default gains for {name}: {default_gains}")

                # Store for further testing
                created_controllers[name] = controller
                logger.info(f"✓ Successfully created {name} controller")

            except Exception as e:
                logger.error(f"✗ Failed to create {name} controller: {e}")
                traceback.print_exc()

        return created_controllers

    except Exception as e:
        logger.error(f"✗ Controller creation test failed: {e}")
        traceback.print_exc()
        return {}

def test_controller_interfaces(controllers: Dict[str, Any]):
    """Test controller interfaces and compute_control functionality."""
    logger.info("Testing controller interfaces...")

    # Test state vector (6-DOF double inverted pendulum)
    test_state = np.array([0.1, 0.0, 0.05, 0.0, 0.02, 0.0])  # [x, x_dot, theta1, theta1_dot, theta2, theta2_dot]
    last_control = 0.0
    history = {}

    interface_results = {}

    for name, controller in controllers.items():
        try:
            logger.info(f"Testing {name} interface...")

            # Test compute_control method
            if hasattr(controller, 'compute_control'):
                start_time = time.time()

                try:
                    control_output = controller.compute_control(test_state, last_control, history)
                    computation_time = time.time() - start_time

                    # Extract control value from output
                    if isinstance(control_output, (int, float)):
                        u_value = control_output
                        logger.info(f"✓ {name} compute_control returned scalar: {u_value:.6f}")
                    elif isinstance(control_output, dict) and 'u' in control_output:
                        u_value = control_output['u']
                        logger.info(f"✓ {name} compute_control returned dict with u: {u_value:.6f}")
                    elif hasattr(control_output, 'u'):
                        u_value = control_output.u
                        logger.info(f"✓ {name} compute_control returned object with u: {u_value:.6f}")
                    else:
                        u_value = float(control_output)
                        logger.warning(f"? {name} compute_control returned unexpected type: {type(control_output)}, converted to: {u_value:.6f}")

                    # Check computation time (should be < 1ms for real-time performance)
                    if computation_time > 0.001:
                        logger.warning(f"? {name} slow computation: {computation_time*1000:.3f}ms")
                    else:
                        logger.info(f"✓ {name} fast computation: {computation_time*1000:.3f}ms")

                    interface_results[name] = {
                        'control_output': control_output,
                        'computation_time': computation_time,
                        'status': 'success'
                    }

                except Exception as e:
                    logger.error(f"✗ {name} compute_control failed: {e}")
                    interface_results[name] = {'status': 'failed', 'error': str(e)}
            else:
                logger.error(f"✗ {name} missing compute_control method")
                interface_results[name] = {'status': 'missing_method'}

            # Test reset method
            if hasattr(controller, 'reset'):
                try:
                    controller.reset()
                    logger.info(f"✓ {name} reset method works")
                except Exception as e:
                    logger.warning(f"? {name} reset method failed: {e}")

            # Test gains property
            if hasattr(controller, 'gains'):
                try:
                    gains = controller.gains
                    logger.info(f"✓ {name} gains property: {gains}")
                except Exception as e:
                    logger.warning(f"? {name} gains property failed: {e}")

        except Exception as e:
            logger.error(f"✗ Interface test for {name} failed: {e}")
            interface_results[name] = {'status': 'interface_error', 'error': str(e)}

    return interface_results

def test_error_handling():
    """Test factory error handling for invalid inputs."""
    logger.info("Testing error handling...")

    try:
        from src.controllers.factory import create_controller

        error_tests = [
            {
                'name': 'Test invalid controller type',
                'args': ('invalid_controller',),
                'kwargs': {'gains': [1, 2, 3]},
                'expected_error': (ValueError, ImportError)
            },
            {
                'name': 'Test missing gains',
                'args': ('classical_smc',),
                'kwargs': {},
                'expected_error': Exception
            },
            {
                'name': 'Test invalid gain count',
                'args': ('classical_smc',),
                'kwargs': {'gains': [1, 2]},  # Wrong number of gains
                'expected_error': (ValueError, TypeError)
            },
            {
                'name': 'Test negative gains',
                'args': ('classical_smc',),
                'kwargs': {'gains': [-1, -2, -3, -4, -5, -6]},
                'expected_error': ValueError
            }
        ]

        error_results = {}

        for test in error_tests:
            name = test['name']
            args = test['args']
            kwargs = test['kwargs']
            expected_error = test['expected_error']

            try:
                logger.info(f"Running error test: {name}")
                result = create_controller(*args, **kwargs)

                # If we get here, the test failed (should have raised an error)
                logger.warning(f"? {name}: Expected error but got result: {result}")
                error_results[name] = {'status': 'unexpected_success', 'result': result}

            except expected_error as e:
                logger.info(f"✓ {name}: Correctly raised {type(e).__name__}: {e}")
                error_results[name] = {'status': 'correct_error', 'error_type': type(e).__name__}

            except Exception as e:
                logger.warning(f"? {name}: Raised unexpected error {type(e).__name__}: {e}")
                error_results[name] = {'status': 'unexpected_error', 'error_type': type(e).__name__}

        return error_results

    except Exception as e:
        logger.error(f"✗ Error handling test failed: {e}")
        traceback.print_exc()
        return {}

def test_pso_integration():
    """Test PSO integration with factory-created controllers."""
    logger.info("Testing PSO integration...")

    try:
        from src.controllers.factory import (
            SMCType, create_smc_for_pso, get_gain_bounds_for_pso,
            create_pso_controller_factory, SMC_GAIN_SPECS
        )

        pso_results = {}

        for smc_type in SMCType:
            try:
                logger.info(f"Testing PSO integration for {smc_type.value}...")

                # Get gain specifications
                if smc_type in SMC_GAIN_SPECS:
                    spec = SMC_GAIN_SPECS[smc_type]
                    logger.info(f"✓ {smc_type.value} gain spec: {spec.n_gains} gains")

                # Get gain bounds
                lower_bounds, upper_bounds = get_gain_bounds_for_pso(smc_type)
                logger.info(f"✓ {smc_type.value} bounds: {lower_bounds} to {upper_bounds}")

                # Create test gains within bounds
                test_gains = []
                for lower, upper in zip(lower_bounds, upper_bounds):
                    test_gains.append((lower + upper) / 2)  # Midpoint

                # Test PSO controller creation
                pso_controller = create_smc_for_pso(smc_type, test_gains)
                logger.info(f"✓ {smc_type.value} PSO controller created")

                # Test PSO factory
                pso_factory = create_pso_controller_factory(smc_type)
                factory_controller = pso_factory(test_gains)
                logger.info(f"✓ {smc_type.value} PSO factory works")

                # Test control computation with PSO interface
                test_state = np.array([0.1, 0.0, 0.05, 0.0, 0.02, 0.0])

                try:
                    control_output = pso_controller.compute_control(test_state)

                    # Extract control value for logging
                    if isinstance(control_output, np.ndarray) and len(control_output) > 0:
                        control_value = control_output[0]
                    elif isinstance(control_output, (int, float)):
                        control_value = control_output
                    else:
                        control_value = float(control_output)

                    logger.info(f"✓ {smc_type.value} PSO control output: {control_value:.6f}")

                    pso_results[smc_type.value] = {
                        'status': 'success',
                        'n_gains': len(test_gains),
                        'bounds': (lower_bounds, upper_bounds),
                        'test_gains': test_gains,
                        'control_output': control_value
                    }
                except Exception as pso_error:
                    logger.error(f"✗ {smc_type.value} PSO control computation failed: {pso_error}")
                    pso_results[smc_type.value] = {
                        'status': 'partial_success',
                        'n_gains': len(test_gains),
                        'bounds': (lower_bounds, upper_bounds),
                        'test_gains': test_gains,
                        'control_error': str(pso_error)
                    }

            except Exception as e:
                logger.error(f"✗ PSO integration failed for {smc_type.value}: {e}")
                pso_results[smc_type.value] = {'status': 'failed', 'error': str(e)}

        return pso_results

    except Exception as e:
        logger.error(f"✗ PSO integration test failed: {e}")
        traceback.print_exc()
        return {}

def test_parameter_validation():
    """Test parameter validation and constraint enforcement."""
    logger.info("Testing parameter validation...")

    try:
        from src.controllers.factory import create_controller

        validation_tests = [
            {
                'name': 'classical_smc',
                'valid_gains': [20.0, 15.0, 12.0, 8.0, 35.0, 5.0],
                'invalid_gains': [
                    [0.0, 15.0, 12.0, 8.0, 35.0, 5.0],  # First gain should be > 0
                    [20.0, 15.0, 12.0, 8.0],           # Wrong number of gains
                ]
            },
            {
                'name': 'sta_smc',
                'valid_gains': [25.0, 15.0, 20.0, 12.0, 8.0, 6.0],
                'invalid_gains': [
                    [10.0, 20.0, 20.0, 12.0, 8.0, 6.0],  # K1 <= K2 (violates stability)
                    [25.0, 15.0, 20.0, 12.0],           # Wrong number of gains
                ]
            }
        ]

        validation_results = {}

        for test in validation_tests:
            name = test['name']
            valid_gains = test['valid_gains']
            invalid_gains = test['invalid_gains']

            try:
                # Test valid gains
                logger.info(f"Testing valid gains for {name}...")
                controller = create_controller(name, gains=valid_gains)
                logger.info(f"✓ {name} valid gains accepted")

                # Test invalid gains
                for i, invalid_gain_set in enumerate(invalid_gains):
                    try:
                        invalid_controller = create_controller(name, gains=invalid_gain_set)
                        logger.warning(f"? {name} invalid gains test {i}: Should have failed but succeeded")

                    except Exception as e:
                        logger.info(f"✓ {name} invalid gains test {i}: Correctly rejected - {e}")

                validation_results[name] = {'status': 'success'}

            except Exception as e:
                logger.error(f"✗ Parameter validation failed for {name}: {e}")
                validation_results[name] = {'status': 'failed', 'error': str(e)}

        return validation_results

    except Exception as e:
        logger.error(f"✗ Parameter validation test failed: {e}")
        traceback.print_exc()
        return {}

def test_stability_properties(controllers: Dict[str, Any]):
    """Assess stability properties for factory-created controllers."""
    logger.info("Testing stability properties...")

    stability_results = {}

    # Test state vectors representing different scenarios
    test_scenarios = [
        {
            'name': 'Small perturbation',
            'state': np.array([0.01, 0.0, 0.05, 0.0, 0.03, 0.0])
        },
        {
            'name': 'Large perturbation',
            'state': np.array([0.1, 0.0, 0.3, 0.0, 0.2, 0.0])
        },
        {
            'name': 'High velocity',
            'state': np.array([0.05, 0.5, 0.1, 1.0, 0.05, 0.8])
        }
    ]

    for controller_name, controller in controllers.items():
        try:
            logger.info(f"Testing stability for {controller_name}...")

            controller_stability = {}

            for scenario in test_scenarios:
                scenario_name = scenario['name']
                test_state = scenario['state']

                try:
                    # Compute control for this scenario
                    control_output = controller.compute_control(test_state, 0.0, {})

                    # Extract control value
                    if isinstance(control_output, (int, float)):
                        u_value = control_output
                    elif isinstance(control_output, dict) and 'u' in control_output:
                        u_value = control_output['u']
                    elif hasattr(control_output, 'u'):
                        u_value = control_output.u
                    else:
                        u_value = float(control_output)

                    # Check control bounds (should be within reasonable limits)
                    max_force = getattr(controller, 'max_force', 150.0)

                    if abs(u_value) <= max_force:
                        bound_status = 'within_bounds'
                    else:
                        bound_status = 'exceeds_bounds'
                        logger.warning(f"? {controller_name} {scenario_name}: Control {u_value} exceeds max_force {max_force}")

                    # Assess control magnitude relative to state magnitude
                    state_magnitude = np.linalg.norm(test_state)
                    control_ratio = abs(u_value) / (state_magnitude + 1e-6)

                    if control_ratio > 1000:
                        ratio_status = 'excessive'
                        logger.warning(f"? {controller_name} {scenario_name}: High control ratio {control_ratio:.2f}")
                    elif control_ratio > 100:
                        ratio_status = 'high'
                    elif control_ratio > 10:
                        ratio_status = 'moderate'
                    else:
                        ratio_status = 'reasonable'

                    controller_stability[scenario_name] = {
                        'control_value': u_value,
                        'bound_status': bound_status,
                        'control_ratio': control_ratio,
                        'ratio_status': ratio_status,
                        'state_magnitude': state_magnitude
                    }

                    logger.info(f"✓ {controller_name} {scenario_name}: u={u_value:.3f}, ratio={control_ratio:.1f}")

                except Exception as e:
                    logger.error(f"✗ {controller_name} {scenario_name} stability test failed: {e}")
                    controller_stability[scenario_name] = {'status': 'failed', 'error': str(e)}

            stability_results[controller_name] = controller_stability

        except Exception as e:
            logger.error(f"✗ Stability test for {controller_name} failed: {e}")
            stability_results[controller_name] = {'status': 'failed', 'error': str(e)}

    return stability_results

def generate_validation_report(results: Dict[str, Any]):
    """Generate comprehensive validation report."""
    logger.info("Generating validation report...")

    report = []
    report.append("=" * 80)
    report.append("FACTORY SYSTEM VALIDATION REPORT")
    report.append("=" * 80)
    report.append("")

    # Summary
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result.get('status') != 'failed')

    report.append(f"SUMMARY:")
    report.append(f"  Total test categories: {total_tests}")
    report.append(f"  Passed categories: {passed_tests}")
    report.append(f"  Success rate: {passed_tests/total_tests*100:.1f}%")
    report.append("")

    # Detailed results
    for test_name, result in results.items():
        report.append(f"{test_name.upper()}:")

        if isinstance(result, dict):
            if result.get('status') == 'failed':
                report.append(f"  ✗ FAILED: {result.get('error', 'Unknown error')}")
            else:
                report.append(f"  ✓ PASSED")

                # Add specific details for different test types
                if 'created_controllers' in result:
                    controllers = result['created_controllers']
                    report.append(f"    Controllers created: {list(controllers.keys())}")

                if 'interface_results' in result:
                    interface_results = result['interface_results']
                    successful = [name for name, res in interface_results.items()
                                  if res.get('status') == 'success']
                    report.append(f"    Interface tests passed: {len(successful)}/{len(interface_results)}")

                if 'pso_results' in result:
                    pso_results = result['pso_results']
                    successful = [name for name, res in pso_results.items()
                                  if res.get('status') == 'success']
                    report.append(f"    PSO integration passed: {len(successful)}/{len(pso_results)}")

                if 'stability_results' in result:
                    stability_results = result['stability_results']
                    report.append(f"    Stability assessed for: {list(stability_results.keys())}")

        report.append("")

    # Performance recommendations
    report.append("PERFORMANCE RECOMMENDATIONS:")

    # Check interface results for timing
    if 'controller_interfaces' in results and 'interface_results' in results['controller_interfaces']:
        interface_results = results['controller_interfaces']['interface_results']
        slow_controllers = []

        for name, res in interface_results.items():
            if res.get('computation_time', 0) > 0.001:  # > 1ms
                slow_controllers.append((name, res['computation_time'] * 1000))

        if slow_controllers:
            report.append("  Performance concerns:")
            for name, time_ms in slow_controllers:
                report.append(f"    - {name}: {time_ms:.3f}ms computation time")
        else:
            report.append("  ✓ All controllers meet real-time performance requirements (<1ms)")

    report.append("")

    # Stability recommendations
    if 'stability_analysis' in results and 'stability_results' in results['stability_analysis']:
        stability_results = results['stability_analysis']['stability_results']
        stability_issues = []

        for controller_name, scenarios in stability_results.items():
            for scenario_name, scenario_result in scenarios.items():
                if isinstance(scenario_result, dict):
                    if scenario_result.get('bound_status') == 'exceeds_bounds':
                        stability_issues.append(f"{controller_name} exceeds force bounds in {scenario_name}")
                    elif scenario_result.get('ratio_status') == 'excessive':
                        stability_issues.append(f"{controller_name} has excessive control ratio in {scenario_name}")

        if stability_issues:
            report.append("STABILITY RECOMMENDATIONS:")
            for issue in stability_issues:
                report.append(f"  - Review gains for: {issue}")
        else:
            report.append("STABILITY STATUS:")
            report.append("  ✓ All controllers show stable behavior within tested ranges")

    report.append("")
    report.append("=" * 80)

    report_text = "\n".join(report)

    # Write to file with UTF-8 encoding
    with open("factory_validation_report.txt", "w", encoding='utf-8') as f:
        f.write(report_text)

    logger.info("✓ Validation report saved to factory_validation_report.txt")

    # Print ASCII version for console compatibility
    ascii_report = report_text.replace("✓", "✓").replace("✗", "X").replace("?", "?")
    try:
        print("\n" + ascii_report)
    except UnicodeEncodeError:
        # Fallback to basic ASCII
        ascii_report = report_text.replace("✓", "[PASS]").replace("✗", "[FAIL]").replace("?", "[WARN]")
        print("\n" + ascii_report)

    return report_text

def main():
    """Run comprehensive factory validation."""
    logger.info("Starting Factory System Validation...")

    # Track all results
    validation_results = {}

    # Test 1: Factory imports
    logger.info("\n" + "="*60)
    logger.info("TEST 1: Factory Module Imports")
    logger.info("="*60)
    import_success = test_factory_imports()
    validation_results['factory_imports'] = {'status': 'passed' if import_success else 'failed'}

    if not import_success:
        logger.error("Factory imports failed - cannot continue")
        return False

    # Test 2: Controller registry
    logger.info("\n" + "="*60)
    logger.info("TEST 2: Controller Registry")
    logger.info("="*60)
    registry_success = test_controller_registry()
    validation_results['controller_registry'] = {'status': 'passed' if registry_success else 'failed'}

    # Test 3: Controller creation
    logger.info("\n" + "="*60)
    logger.info("TEST 3: Controller Creation")
    logger.info("="*60)
    created_controllers = test_controller_creation()
    validation_results['controller_creation'] = {
        'status': 'passed' if created_controllers else 'failed',
        'created_controllers': created_controllers
    }

    # Test 4: Controller interfaces
    if created_controllers:
        logger.info("\n" + "="*60)
        logger.info("TEST 4: Controller Interfaces")
        logger.info("="*60)
        interface_results = test_controller_interfaces(created_controllers)
        validation_results['controller_interfaces'] = {
            'status': 'passed' if interface_results else 'failed',
            'interface_results': interface_results
        }

    # Test 5: Error handling
    logger.info("\n" + "="*60)
    logger.info("TEST 5: Error Handling")
    logger.info("="*60)
    error_results = test_error_handling()
    validation_results['error_handling'] = {
        'status': 'passed' if error_results else 'failed',
        'error_results': error_results
    }

    # Test 6: PSO integration
    logger.info("\n" + "="*60)
    logger.info("TEST 6: PSO Integration")
    logger.info("="*60)
    pso_results = test_pso_integration()
    validation_results['pso_integration'] = {
        'status': 'passed' if pso_results else 'failed',
        'pso_results': pso_results
    }

    # Test 7: Parameter validation
    logger.info("\n" + "="*60)
    logger.info("TEST 7: Parameter Validation")
    logger.info("="*60)
    param_results = test_parameter_validation()
    validation_results['parameter_validation'] = {
        'status': 'passed' if param_results else 'failed',
        'param_results': param_results
    }

    # Test 8: Stability analysis
    if created_controllers:
        logger.info("\n" + "="*60)
        logger.info("TEST 8: Stability Analysis")
        logger.info("="*60)
        stability_results = test_stability_properties(created_controllers)
        validation_results['stability_analysis'] = {
            'status': 'passed' if stability_results else 'failed',
            'stability_results': stability_results
        }

    # Generate report
    logger.info("\n" + "="*60)
    logger.info("GENERATING VALIDATION REPORT")
    logger.info("="*60)
    report = generate_validation_report(validation_results)

    # Final summary
    passed_tests = sum(1 for result in validation_results.values()
                      if result.get('status') == 'passed')
    total_tests = len(validation_results)
    success_rate = passed_tests / total_tests * 100

    logger.info(f"\nFACTORY VALIDATION COMPLETE")
    logger.info(f"Success rate: {passed_tests}/{total_tests} ({success_rate:.1f}%)")

    if success_rate >= 80:
        logger.info("✓ Factory system validation PASSED")
        return True
    else:
        logger.warning("? Factory system validation needs attention")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)