# Example from: docs\factory\configuration_migration_mathematical_foundations.md
# Index: 7
# Runnable: False
# Hash: 55d06efc

class MigrationValidationSuite:
    """Comprehensive test suite for migration validation."""

    def __init__(self):
        self.test_results = []

    def run_full_validation(self, old_config: Dict[str, Any], new_config: Dict[str, Any], controller_type: str) -> Dict[str, Any]:
        """Run comprehensive migration validation."""

        results = {
            'controller_type': controller_type,
            'migration_successful': True,
            'tests': {},
            'warnings': [],
            'errors': []
        }

        # Test 1: Parameter count validation
        results['tests']['parameter_count'] = self.test_parameter_count(old_config, new_config, controller_type)

        # Test 2: Stability preservation
        results['tests']['stability'] = self.test_stability_preservation(new_config, controller_type)

        # Test 3: Physical realizability
        results['tests']['physical_realizability'] = self.test_physical_realizability(new_config, controller_type)

        # Test 4: Performance preservation
        results['tests']['performance'] = self.test_performance_preservation(old_config, new_config, controller_type)

        # Test 5: Numerical stability
        results['tests']['numerical_stability'] = self.test_numerical_stability(new_config, controller_type)

        # Aggregate results
        failed_tests = [name for name, result in results['tests'].items() if not result.get('passed', False)]
        results['migration_successful'] = len(failed_tests) == 0

        if failed_tests:
            results['errors'].extend([f"Failed test: {test}" for test in failed_tests])

        return results

    def test_parameter_count(self, old_config: Dict[str, Any], new_config: Dict[str, Any], controller_type: str) -> Dict[str, Any]:
        """Test parameter count migration."""

        expected_counts = {
            'classical_smc': 6,
            'adaptive_smc': 5,
            'sta_smc': 6,
            'hybrid_adaptive_sta_smc': 4
        }

        new_gains = new_config.get('gains', [])
        expected_count = expected_counts.get(controller_type, 0)

        passed = len(new_gains) == expected_count

        return {
            'passed': passed,
            'expected_count': expected_count,
            'actual_count': len(new_gains),
            'gains': new_gains
        }

    def test_stability_preservation(self, new_config: Dict[str, Any], controller_type: str) -> Dict[str, Any]:
        """Test stability preservation."""

        gains = new_config.get('gains', [])

        if controller_type == 'classical_smc':
            return StabilityValidator.validate_classical_smc_stability(gains)
        elif controller_type == 'adaptive_smc':
            adaptation_params = {
                'leak_rate': new_config.get('leak_rate', 0.01),
                'K_min': new_config.get('K_min', 0.1),
                'K_max': new_config.get('K_max', 100.0)
            }
            return StabilityValidator.validate_adaptive_smc_convergence(gains, adaptation_params)
        elif controller_type == 'sta_smc':
            algorithm_params = {
                'power_exponent': new_config.get('power_exponent', 0.5)
            }
            return StabilityValidator.validate_sta_smc_finite_time_convergence(gains, algorithm_params)

        return {'passed': True, 'reason': 'No stability test for this controller type'}

    def test_physical_realizability(self, new_config: Dict[str, Any], controller_type: str) -> Dict[str, Any]:
        """Test physical realizability of parameters."""

        gains = new_config.get('gains', [])
        max_force = new_config.get('max_force', 150.0)
        dt = new_config.get('dt', 0.001)

        issues = []

        # Check gain magnitudes
        if any(g > 1000 for g in gains):
            issues.append("Extremely high gains may be unrealistic")

        # Check sampling time
        if dt < 1e-4:  # Less than 0.1ms
            issues.append(f"Very fast sampling time dt={dt}s may be unrealistic")
        elif dt > 0.1:  # More than 100ms
            issues.append(f"Slow sampling time dt={dt}s may degrade performance")

        # Check actuator limits
        if max_force > 1000:  # More than 1kN
            issues.append(f"High force limit {max_force}N may be unrealistic")
        elif max_force < 1:  # Less than 1N
            issues.append(f"Low force limit {max_force}N may be insufficient")

        return {
            'passed': len(issues) == 0,
            'issues': issues,
            'parameters_checked': ['gains', 'max_force', 'dt']
        }

    def test_performance_preservation(self, old_config: Dict[str, Any], new_config: Dict[str, Any], controller_type: str) -> Dict[str, Any]:
        """Test performance preservation."""

        bandwidth_analysis = PerformanceAnalyzer.analyze_control_bandwidth(
            old_config.get('gains', []),
            new_config.get('gains', []),
            controller_type
        )

        settling_analysis = PerformanceAnalyzer.estimate_settling_time_change(old_config, new_config)

        # Performance is preserved if bandwidth and settling time are reasonable
        bandwidth_ok = bandwidth_analysis.get('performance_preserved', True)
        settling_ok = settling_analysis.get('performance_change') in ['improved', 'maintained']

        return {
            'passed': bandwidth_ok and settling_ok,
            'bandwidth_analysis': bandwidth_analysis,
            'settling_analysis': settling_analysis
        }

    def test_numerical_stability(self, new_config: Dict[str, Any], controller_type: str) -> Dict[str, Any]:
        """Test numerical stability of parameters."""

        gains = new_config.get('gains', [])
        dt = new_config.get('dt', 0.001)

        issues = []

        # Check condition numbers and numerical issues
        if controller_type in ['classical_smc', 'adaptive_smc', 'sta_smc']:
            if len(gains) >= 4:
                k1, k2, lam1, lam2 = gains[:4]

                # Check gain ratios for numerical stability
                if lam1/k1 > 100 or lam2/k2 > 100:
                    issues.append("High λ/k ratios may cause numerical instability")

                if k1/k2 > 10 or k2/k1 > 10:
                    issues.append("Large k1/k2 ratio may indicate unbalanced design")

        # Check discrete-time stability
        if controller_type in ['adaptive_smc', 'sta_smc']:
            max_gain = max(gains) if gains else 0
            nyquist_limit = 1.0 / (2 * dt)
            if max_gain > nyquist_limit / 10:  # Rule of thumb
                issues.append(f"High gains relative to sampling rate may cause instability")

        return {
            'passed': len(issues) == 0,
            'issues': issues,
            'sampling_time': dt,
            'stability_margins': 'acceptable' if len(issues) == 0 else 'marginal'
        }

# Full validation example
migration_suite = MigrationValidationSuite()

old_config = {
    'gains': [20, 15, 12, 8, 35],
    'K_switching': 5.0,
    'switch_function': 'sign'
}

new_config = {
    'gains': [20, 15, 12, 8, 35, 5.0],
    'switch_method': 'sign',
    'boundary_layer': 0.02,
    'max_force': 150.0,
    'dt': 0.001
}

validation_results = migration_suite.run_full_validation(old_config, new_config, 'classical_smc')
print("Migration validation results:")
for test_name, result in validation_results['tests'].items():
    status = "✅ PASS" if result.get('passed', False) else "❌ FAIL"
    print(f"  {test_name}: {status}")

if validation_results['migration_successful']:
    print("✅ Migration validation SUCCESSFUL")
else:
    print("❌ Migration validation FAILED")
    for error in validation_results['errors']:
        print(f"  - {error}")