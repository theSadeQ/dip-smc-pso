# Example from: docs\pso_configuration_schema_documentation.md
# Index: 2
# Runnable: False
# Hash: da8cd51c

# example-metadata:
# runnable: false

class DynamicBoundsSelector:
    """
    Intelligent bounds selection based on controller type and system requirements.
    """

    def __init__(self, config_schema: dict):
        self.base_bounds = config_schema['bounds']
        self.controller_bounds = {
            key: value for key, value in config_schema['bounds'].items()
            if key not in ['base', 'min', 'max']
        }

    def get_bounds_for_controller(self, controller_type: str,
                                dynamic_adjustment: bool = True) -> dict:
        """
        Get optimized bounds for specific controller type.

        Parameters:
        controller_type: SMC variant identifier
        dynamic_adjustment: Enable runtime bounds optimization

        Returns:
        dict: Complete bounds specification with validation rules
        """
        # Start with controller-specific bounds
        if controller_type in self.controller_bounds:
            bounds = self.controller_bounds[controller_type].copy()
        else:
            # Fallback to default bounds
            bounds = {
                'min': self.base_bounds['min'],
                'max': self.base_bounds['max']
            }

        # Apply dynamic adjustments if enabled
        if dynamic_adjustment:
            bounds = self._apply_dynamic_adjustments(bounds, controller_type)

        # Add validation constraints
        bounds['validation_rules'] = self._get_validation_rules(controller_type)

        return bounds

    def _apply_dynamic_adjustments(self, bounds: dict, controller_type: str) -> dict:
        """
        Apply runtime bounds optimization based on system state and performance.
        """
        if controller_type == 'sta_smc':
            # Issue #2 specific adjustments
            current_performance = self._assess_current_performance()
            if current_performance.overshoot > 0.05:  # >5% overshoot
                # Further restrict lambda bounds
                bounds['max'][4] = min(bounds['max'][4], 5.0)  # lambda1
                bounds['max'][5] = min(bounds['max'][5], 5.0)  # lambda2

        return bounds

    def _get_validation_rules(self, controller_type: str) -> list:
        """
        Get controller-specific validation rules for PSO bounds enforcement.
        """
        rules = ['positive_gains', 'actuator_saturation']

        if controller_type == 'sta_smc':
            rules.extend(['k1_greater_k2', 'finite_time_convergence', 'issue2_overshoot'])
        elif controller_type == 'adaptive_smc':
            rules.extend(['adaptation_stability'])
        elif controller_type == 'classical_smc':
            rules.extend(['damping_ratio_bounds'])

        return rules