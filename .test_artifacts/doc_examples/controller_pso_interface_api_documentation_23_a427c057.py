# Example from: docs\controller_pso_interface_api_documentation.md
# Index: 23
# Runnable: False
# Hash: a427c057

# example-metadata:
# runnable: false

def legacy_controller_adapter(legacy_controller_class):
    """Adapter for legacy controllers without PSO interface."""

    class PSO_CompatibleAdapter(PSO_ControllerInterface):
        def __init__(self, gains: np.ndarray, **kwargs):
            # Convert gains to legacy format
            legacy_params = self._convert_gains_to_legacy(gains)
            self._legacy_controller = legacy_controller_class(**legacy_params)
            self._max_force = kwargs.get('max_force', 150.0)

        @property
        def max_force(self) -> float:
            return self._max_force

        def compute_control(self, state: np.ndarray, **kwargs) -> float:
            return self._legacy_controller.compute_control(state, **kwargs)

        def _convert_gains_to_legacy(self, gains: np.ndarray) -> dict:
            # Implementation-specific conversion
            pass

    return PSO_CompatibleAdapter

# Usage:
# PSO_CompatibleLegacyController = legacy_controller_adapter(LegacyControllerClass)