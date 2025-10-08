# Example from: docs\factory\controller_integration_guide.md
# Index: 10
# Runnable: False
# Hash: d98a17e0

class ControllerIntegrationValidator:
    """Comprehensive validation of controller-factory-plant integration."""

    def __init__(self, plant_config: Any):
        self.plant_config = plant_config
        self.test_states = self._generate_test_states()

    def _generate_test_states(self) -> Dict[str, StateVector]:
        """Generate comprehensive test states for validation."""
        return {
            'equilibrium': np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
            'small_disturbance': np.array([0.1, 0.05, 0.03, 0.0, 0.0, 0.0]),
            'large_angles': np.array([0.5, 0.8, 0.6, 0.2, 0.1, 0.15]),
            'high_velocity': np.array([0.1, 0.1, 0.1, 2.0, 1.5, 1.2]),
            'extreme_state': np.array([1.0, 1.2, 0.9, 3.0, 2.5, 2.0])
        }

    def validate_controller_integration(
        self,
        controller_type: str,
        gains: GainsArray
    ) -> Dict[str, Any]:
        """Comprehensive integration validation."""

        results = {
            'controller_type': controller_type,
            'gains': gains,
            'creation_success': False,
            'control_computation_success': False,
            'stability_analysis': {},
            'performance_metrics': {},
            'integration_score': 0.0
        }

        try:
            # 1. Controller creation test
            controller = create_controller(controller_type, self.plant_config, gains)
            results['creation_success'] = True

            # 2. Control computation test
            control_results = {}
            for state_name, state in self.test_states.items():
                try:
                    control = controller.compute_control(state, (), {})
                    control_results[state_name] = {
                        'success': True,
                        'control_magnitude': np.abs(control.u) if hasattr(control, 'u') else np.abs(control),
                        'within_bounds': np.abs(control.u if hasattr(control, 'u') else control) <= 200.0
                    }
                except Exception as e:
                    control_results[state_name] = {
                        'success': False,
                        'error': str(e)
                    }

            results['control_computation_success'] = all(
                result['success'] for result in control_results.values()
            )
            results['control_results'] = control_results

            # 3. PSO wrapper test
            try:
                pso_wrapper = create_pso_optimized_controller(
                    controller_type, gains, self.plant_config
                )

                pso_test_results = {}
                for state_name, state in self.test_states.items():
                    control_array = pso_wrapper.compute_control(state)
                    pso_test_results[state_name] = {
                        'control_shape': control_array.shape,
                        'control_value': control_array[0],
                        'within_saturation': np.abs(control_array[0]) <= pso_wrapper.max_force
                    }

                results['pso_integration_success'] = True
                results['pso_test_results'] = pso_test_results

            except Exception as e:
                results['pso_integration_success'] = False
                results['pso_error'] = str(e)

            # 4. Calculate integration score
            score = 0.0
            if results['creation_success']:
                score += 25.0
            if results['control_computation_success']:
                score += 25.0
            if results['pso_integration_success']:
                score += 25.0

            # Additional scoring based on control quality
            successful_controls = sum(
                1 for result in control_results.values() if result['success']
            )
            score += (successful_controls / len(control_results)) * 25.0

            results['integration_score'] = score

        except Exception as e:
            results['creation_error'] = str(e)

        return results

    def run_full_integration_suite(
        self,
        controller_configs: List[Tuple[str, GainsArray]]
    ) -> Dict[str, Any]:
        """Run full integration test suite for multiple controllers."""

        suite_results = {
            'test_timestamp': time.time(),
            'plant_config_type': type(self.plant_config).__name__,
            'controller_results': {},
            'summary': {}
        }

        total_score = 0.0
        successful_integrations = 0

        for controller_type, gains in controller_configs:
            result = self.validate_controller_integration(controller_type, gains)
            suite_results['controller_results'][controller_type] = result

            total_score += result['integration_score']
            if result['integration_score'] >= 75.0:  # 75% threshold for success
                successful_integrations += 1

        suite_results['summary'] = {
            'total_controllers_tested': len(controller_configs),
            'successful_integrations': successful_integrations,
            'success_rate': successful_integrations / len(controller_configs),
            'average_integration_score': total_score / len(controller_configs),
            'overall_status': 'PASS' if successful_integrations >= len(controller_configs) * 0.8 else 'FAIL'
        }

        return suite_results

# Example usage:
validator = ControllerIntegrationValidator(simplified_plant_config)

test_configs = [
    ('classical_smc', [20.0, 15.0, 12.0, 8.0, 35.0, 5.0]),
    ('adaptive_smc', [25.0, 18.0, 15.0, 12.0, 3.5]),
    ('sta_smc', [35.0, 20.0, 25.0, 18.0, 12.0, 8.0]),
    ('hybrid_adaptive_sta_smc', [15.0, 12.0, 10.0, 8.0])
]

integration_results = validator.run_full_integration_suite(test_configs)