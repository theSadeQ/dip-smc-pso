# Example from: docs\technical\pso_integration_workflows.md
# Index: 12
# Runnable: False
# Hash: bb4af99d

def _evaluate_controller_performance(self, controller, gains):
    """Multi-scenario performance evaluation."""

    # For each test scenario:
    for scenario in test_scenarios:
        # Simulate controller performance
        cost = self._simulate_scenario(controller, scenario)
        total_cost += cost * scenario['weight']

    # Cost components:
    # - Position error: 10.0 * ∫|state_error|²dt
    # - Control effort: 0.1 * ∫|u|²dt
    # - Control rate: 0.05 * ∫|du/dt|²dt
    # - Stability penalty: penalties for instability

    return total_cost / total_weight