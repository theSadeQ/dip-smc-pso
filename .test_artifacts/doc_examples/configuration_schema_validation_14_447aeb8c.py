# Example from: docs\configuration_schema_validation.md
# Index: 14
# Runnable: True
# Hash: 447aeb8c

class RuntimeConfigValidator:
    """Real-time configuration validation system."""

    def __init__(self, base_config: dict):
        self.base_config = MasterConfig(**base_config)
        self.validation_cache = {}

    def validate_parameter_update(self, parameter_path: str, new_value: any) -> bool:
        """Validate real-time parameter updates."""

        # Parse parameter path (e.g., "controllers.classical_smc.gains.0")
        path_parts = parameter_path.split('.')

        # Create temporary config with updated value
        temp_config = self._update_config_path(self.base_config.dict(), path_parts, new_value)

        try:
            # Validate complete configuration
            MasterConfig(**temp_config)

            # Additional runtime checks
            self._validate_runtime_constraints(parameter_path, new_value, temp_config)

            return True

        except ValidationError as e:
            raise ValueError(f"Parameter update validation failed: {e}")

    def _validate_runtime_constraints(self, param_path: str, value: any, config: dict) -> None:
        """Additional runtime-specific validation."""

        # Control stability constraints during operation
        if 'gains' in param_path:
            controller_name = param_path.split('.')[1]
            self._validate_gain_update_stability(controller_name, config)

        # Optimization parameter updates
        if 'optimization' in param_path:
            self._validate_optimization_update(config)

        # Safety parameter updates
        if 'saturation_limit' in param_path:
            self._validate_saturation_update(value)

    def _validate_gain_update_stability(self, controller_name: str, config: dict) -> None:
        """Validate controller gain updates for continued stability."""

        controller_config = config['controllers'][controller_name]

        if controller_name == 'classical_smc':
            gains = controller_config['gains']
            lambda1, lambda2 = gains[0], gains[1]

            # Real-time stability check
            if lambda1 <= 0 or lambda2 <= 0:
                raise ValueError("Gain update would destabilize system")

            # Check if new gains are too different from current
            current_gains = self.base_config.controllers[controller_name]['gains']
            max_change_ratio = 2.0  # Allow 2x change maximum

            for new_gain, current_gain in zip(gains, current_gains):
                change_ratio = new_gain / current_gain
                if change_ratio > max_change_ratio or change_ratio < 1/max_change_ratio:
                    raise ValueError(f"Gain change ratio {change_ratio:.2f} too large")

    def _update_config_path(self, config: dict, path_parts: list, value: any) -> dict:
        """Update configuration at specified path."""
        import copy
        updated_config = copy.deepcopy(config)

        current = updated_config
        for part in path_parts[:-1]:
            if part.isdigit():
                current = current[int(part)]
            else:
                current = current[part]

        final_key = path_parts[-1]
        if final_key.isdigit():
            current[int(final_key)] = value
        else:
            current[final_key] = value

        return updated_config